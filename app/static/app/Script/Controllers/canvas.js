$(function () {
    var canvas = document.querySelector("canvas");
    canvas.width = window.innerWidth-100;
    canvas.height =  window.innerHeight ;
    var comopnent = canvas.getContext('2d');
    var _topSilde={
        x:50,
        y:50,
        w:30,
        h:360,
        r:150
    };
    var _bottomSilde={
        x:canvas.width- _topSilde.w-50,
        y:canvas.height- _topSilde.h-50,
        w:30,
        h:360,
        r:(_topSilde.h-_topSilde.w)
    };
    var animateConfig={
        dXtop: 0.5,
        dXbottom: 0.5,
        dYtop: 0.5,
        dYbottom: 0.5,
        Xtop:_topSilde.x,
        Ytop:_topSilde.y,
        Xbottom:_bottomSilde.x,
        Ybottom:_bottomSilde.y,
        turn: 1,
        text_interval:5,
        base: 0

    };
    var subTitle={
        current: "",
        pos: 0,
        end: "Find the prefect match!",
        writer:"|",
        writer_interval:40,
        base: 0
    };
    function createBorder(){
            comopnent.clearRect(0,0,canvas.width,innerHeight);
            comopnent.fillRect(animateConfig.Xtop, animateConfig.Ytop, _topSilde.w, _topSilde.h);
            comopnent.fillRect(animateConfig.Xtop, animateConfig.Ytop, _topSilde.h-_topSilde.r, _topSilde.w);
            comopnent.fillRect(animateConfig.Xbottom, animateConfig.Ybottom, _topSilde.w, _topSilde.h);
            comopnent.fillRect(animateConfig.Xbottom-_bottomSilde.r+_topSilde.r, animateConfig.Ybottom+_bottomSilde.r,_topSilde.h-_topSilde.r, _topSilde.w);
        
        
            if(animateConfig.turn==1){    
                if(animateConfig.Xtop>_topSilde.x || animateConfig.Xtop<0){
                    animateConfig.dXtop=-animateConfig.dXtop;
                    animateConfig.turn=0;
                }
                animateConfig.Xtop+=animateConfig.dXtop;
            
                if(animateConfig.Ytop>_topSilde.y || animateConfig.Ytop<0){
                    animateConfig.dYtop=-animateConfig.dYtop;
                    animateConfig.turn=0;
                }
            animateConfig.Ytop+=animateConfig.dYtop;
            }   
            else{
                if(animateConfig.Xbottom>canvas.width-_bottomSilde.w|| animateConfig.Xbottom<_bottomSilde.x){
                    animateConfig.dXbottom=-animateConfig.dXbottom;
                    animateConfig.turn=1;
                }
                animateConfig.Xbottom+=animateConfig.dXbottom;
            
                if(animateConfig.Ybottom>innerHeight-_bottomSilde.h || animateConfig.Ybottom<_bottomSilde.y){
                    animateConfig.dYbottom=-animateConfig.dYbottom;
                    animateConfig.turn=1;
                }
                animateConfig.Ybottom+=animateConfig.dYbottom;
            }
    }
    function updateSubTitle(){
        if(subTitle.current!=subTitle.end)
        {
            subTitle.current+=subTitle.end[subTitle.pos];
            subTitle.pos++;
        }

    }
    function createTitle(){
        comopnent.font = "oblique lighter 40px Berlin Sans FB Demi";
        comopnent.textAlign = "center";
        comopnent.strokeStyle='#686868';
        comopnent.strokeText(subTitle.current+subTitle.writer, canvas.width/2, canvas.height/2+100); 
        comopnent.font = "bold 166px Agency FB";
        comopnent.textAlign = "center";
        comopnent.shadowColor = "#00D4FF"
        comopnent.shadowBlur = 4;
        comopnent.fillText("JobMatch", canvas.width/2, canvas.height/2); 
        comopnent.shadowBlur = 0;
        if(animateConfig.base++ >=animateConfig.text_interval)
        {
            if(subTitle.current!=subTitle.end)
            {
                updateSubTitle();
            }
            animateConfig.base=0;
        }
        if(subTitle.current==subTitle.end)
        {
            if(subTitle.base++>subTitle.writer_interval)
            subTitle.base=0;

            else if(subTitle.base>subTitle.writer_interval/4
                && subTitle.base<subTitle.writer_interval/2)
                {
                    subTitle.writer=" ";
                }
                else
                {
                    subTitle.writer="|";
                }
        }
         
        
       
    }

    function animate(){
        requestAnimationFrame(animate);
        createBorder();
        createTitle();
    }
       
    animate();
    
});    
    
